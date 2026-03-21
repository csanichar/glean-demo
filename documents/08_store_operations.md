# Volta Coffee Co. — Store Operations Manual

**Document ID:** OPS-001  
**Last Updated:** 2026-02-25  
**Owner:** Retail Operations  
**Classification:** Internal Use Only

## Store Hours

| Location | Monday–Friday | Saturday–Sunday |
|----------|--------------|-----------------|
| Williamsburg (Flagship) | 6:30 AM – 8:00 PM | 7:00 AM – 8:00 PM |
| Park Slope | 7:00 AM – 7:00 PM | 7:30 AM – 6:00 PM |
| Lower East Side | 7:00 AM – 7:00 PM | 7:30 AM – 6:00 PM |
| Red Hook (Roastery + Café) | 8:00 AM – 5:00 PM | 8:00 AM – 4:00 PM |
| Midtown (Opening Q2 2026) | TBD | TBD |

Holiday hours are posted 2 weeks in advance in the #retail-ops Slack channel and on the employee portal. All locations are closed on Thanksgiving and Christmas Day.

## Opening Procedures

The opening barista arrives 30 minutes before store open. Follow this sequence:

1. **Disarm the alarm system** using the code stored in 1Password under "Store Alarms — [Location Name]."
2. **Inspect the store:** Walk the floor. Check for any overnight issues (water leaks, equipment malfunctions, pest activity). Report anything abnormal to the Store Manager immediately.
3. **Turn on equipment:**
   - Espresso machine (La Marzocco Linea PB) — already on timer, verify it's at operating temperature (200°F ± 2°F).
   - Grinders — purge 5g of beans, then calibrate per BREW-001.
   - Batch brewer — run a blank water cycle to flush, then brew the first batch.
   - Cold brew taps — check keg pressure (30 PSI for nitro, 12 PSI for still).
4. **Prep station setup:**
   - Stock milk (whole, oat, almond) in the under-counter fridge. Minimum 4 gallons whole milk for weekday open.
   - Fill syrup bottles from bulk containers. Check expiration dates.
   - Set out pastry case items per the daily order from Blue Sky Bakery.
   - Fill ice bins.
5. **POS check:** Open all registers in Toast. Verify cash drawer ($150 starting bank, confirmed by count).
6. **Water quality check:** Run a TDS reading. Log in the Water Quality Tracker. If TDS is outside 120–150 ppm, contact the Facilities team before serving.
7. **Unlock the door at exactly the posted opening time.**

## Closing Procedures

The closing barista stays 30 minutes after store close. Follow this sequence:

1. **Last call:** Announce last call for orders 15 minutes before close.
2. **Lock the front door** at the posted closing time.
3. **Clean all equipment:**
   - Backflush the espresso machine with Cafiza (3 cycles per group head).
   - Disassemble and soak portafilter baskets and steam wand tips.
   - Wipe down grinders. Do NOT use water on the grinder burrs.
   - Clean the batch brewer with Urnex.
   - Wipe down all counters, sinks, and the pastry case.
4. **Restock for tomorrow:**
   - Move 2 bags of beans from storage to the bar area.
   - Check pastry order for the next day (submitted in BlueCart by 2:00 PM).
   - Restock cups, lids, sleeves, napkins.
5. **Cash handling:**
   - Count the cash drawer. Record the count in Toast.
   - Any discrepancy over $5.00 must be reported to the Store Manager.
   - Place cash in the safe. Do NOT leave cash in the register overnight.
6. **Final walkthrough:** Check restrooms, back of house, and outdoor seating area. All tables wiped, chairs pushed in, trash emptied.
7. **Set the alarm system** and lock the door. Confirm the alarm is armed (solid green light on the panel).

## Staffing Model

### Minimum Staffing by Daypart

| Daypart | Hours | Minimum Staff | Roles |
|---------|-------|--------------|-------|
| Morning Rush | Open – 10:00 AM | 3 | 1 Bar, 1 Support/Float, 1 Register |
| Midday | 10:00 AM – 2:00 PM | 2 | 1 Bar, 1 Register/Support |
| Afternoon | 2:00 PM – 5:00 PM | 2 | 1 Bar, 1 Register/Support |
| Evening | 5:00 PM – Close | 1–2 | 1 Bar (+ 1 if volume warrants) |

Weekend morning rush requires an additional staff member (4 total) at the Williamsburg and Park Slope locations.

### Scheduling

- Schedules are published in Homebase by Wednesday for the following week.
- Shift swaps must be arranged through Homebase and approved by the Shift Lead or Store Manager. Direct swaps without system approval are not permitted.
- Overtime (over 40 hours/week) requires pre-approval from the Store Manager.

## Inventory Management

### Daily Counts

Count the following items daily at close:
- Whole bean coffee (bags on hand by SKU)
- Milk inventory (gallons by type)
- Pastry count (for waste tracking and next-day ordering)
- Cup and lid inventory

Log counts in the Inventory Tracker (Notion). The inventory-service pulls this data nightly for analytics.

### Ordering

- **Green coffee and roasted beans:** Managed by the Roasting team. Retail locations submit requests via #supply-chain Slack channel if running low outside the normal delivery schedule.
- **Milk and perishables:** Auto-ordered through BlueCart based on par levels. Store Manager adjusts par levels seasonally.
- **Dry goods and supplies:** Ordered weekly through BlueCart. Delivery on Tuesdays.
- **Pastries:** Daily order submitted by 2:00 PM for next-morning delivery from Blue Sky Bakery.

### Waste Tracking

All waste is logged in the Waste Tracker (Notion) with category:
- **Expired:** Product past shelf life
- **Quality:** Pulled for quality reasons (stale batch brew, improperly steamed milk, etc.)
- **Damaged:** Broken cups, dropped pastries, etc.
- **Overproduction:** Batch brew or cold brew not sold within hold time

The data-pipeline aggregates waste data weekly for review by the Retail Operations team. Locations with waste exceeding 8% of cost of goods sold trigger a review.

## Equipment Maintenance

### Daily
- Backflush espresso machine (closing)
- Clean grinder hoppers and chutes
- Sanitize steam wands after every use

### Weekly
- Deep clean espresso machine (soak group head screens, replace gaskets if worn)
- Calibrate batch brewer against BREW-001 specs
- Clean cold brew taps and lines with BLC

### Monthly
- Replace water filtration cartridges (or as indicated by the filter monitor)
- Inspect grinder burrs for wear (replace every 600–800 lbs of coffee)
- HVAC filter check

### Equipment Failures
- For Toast POS issues: Contact Toast support at 1-888-535-0606.
- For espresso machine issues: Contact La Marzocco USA service at the number in 1Password. Do NOT attempt to repair electrical or plumbing components.
- For grinder issues: Contact the in-house Equipment Tech via #equipment Slack channel.
- If a critical piece of equipment (espresso machine, batch brewer, or POS) is down, notify the Store Manager immediately. The Store Manager determines whether to remain open with a reduced menu or close temporarily.
