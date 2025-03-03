from pulp import LpProblem, LpMinimize, LpVariable, lpSum
from .models import Hospital, MedicalSupply, DistributionRecord

def optimize_distribution():
    hospitals = Hospital.objects.all()
    supplies = MedicalSupply.objects.all()

    if not hospitals.exists() or not supplies.exists():
        return {"error": "No hospitals or medical supplies available"}

    # Define the LP problem
    prob = LpProblem("Medical_Supply_Distribution", LpMinimize)

    # Decision variables: Quantity of each supply allocated to each hospital
    allocation = {}
    for hospital in hospitals:
        for supply in supplies:
            allocation[(hospital.id, supply.id)] = LpVariable(
                f"alloc_{hospital.id}_{supply.id}", lowBound=0, cat="Integer"
            )

    # Objective function: Minimize total cost
    prob += lpSum(
        allocation[(hospital.id, supply.id)] * supply.cost_per_unit
        for hospital in hospitals for supply in supplies
    )

    # Constraints: Meet hospital demand without exceeding availability
    for hospital in hospitals:
        prob += lpSum(allocation[(hospital.id, supply.id)] for supply in supplies) >= (
            hospital.demand_masks + hospital.demand_gloves + 
            hospital.demand_syringes + hospital.demand_ventilators
        )  # Total demand constraint

    for supply in supplies:
        prob += lpSum(allocation[(hospital.id, supply.id)] for hospital in hospitals) <= supply.available_quantity

    # Solve the optimization problem
    prob.solve()

    # Save results in the database
    DistributionRecord.objects.all().delete()  # Clear previous records
    for hospital in hospitals:
        for supply in supplies:
            allocated_qty = allocation[(hospital.id, supply.id)].varValue
            if allocated_qty > 0:
                hospital_obj = Hospital.objects.filter(id=hospital.id).first()  # Ensure hospital exists
                supply_obj = MedicalSupply.objects.filter(id=supply.id).first()

                if hospital_obj and supply_obj:
                    DistributionRecord.objects.create(
                        hospital=hospital_obj,  # Ensure a valid hospital object is assigned
                        supply=supply_obj,
                        allocated_quantity=int(allocated_qty),
                        cost=int(allocated_qty * supply.cost_per_unit)
                    )



    return {"status": "Optimization completed successfully"}
