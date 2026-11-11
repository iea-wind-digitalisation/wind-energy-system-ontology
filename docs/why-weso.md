# Why WESO exists

## One string, several meanings

Ask three people at a wind farm what "the gearbox of T07" is and you can get three correct answers:

- the **slot** in the turbine that has held a gearbox since 2019, whatever is bolted into it today;
- the **41-tonne machine**, serial 000-00-125, currently sitting in that slot;
- the **product**, ACME GB-4200, of which that machine is one copy.

In conversation nobody is confused. "The gearbox failed three times" obviously means the slot (three different machines). "The gearbox weighs 41 tonnes" obviously means the machine. "The gearbox has a known lubrication issue" obviously means the product.

Data systems are not so forgiving. Each one picks a meaning — often several — and bakes it into its identifiers:

| System | Its identifier names… |
|---|---|
| RDS function aspect (`=A1=JF2`) | a slot in a functional breakdown |
| RDS product aspect (`-A1-JF1`) | a slot in a product breakdown — a *different* tree |
| RDS site aspect (`++…`) | a space |
| Manufacturer part number (`GB4200`) | a product specification |
| Serial number (`000-00-125`) | one physical machine |
| Failure-statistics category ("Gearbox") | a bucket for counting |
| SCADA logical node (`WTRM1`) | a measurement grouping that spans more than one slot |

None of these is wrong. They answer different questions. The trouble starts when data from two of them meet.

## What goes wrong when they meet

**Counting.** A turbine has three blades. If one blade is replaced, a database that counts *units* now sees four blade-lives on a three-blade machine; one that counts *turbines* sees one blade population where there are three. Failure rates computed either way are wrong, and nothing in the data flags it.

**Pooling.** Two operators want to pool reliability data. Their manufacturers extended the designation standard differently below the level it standardises, so the same kind of planet bearing has different tags. Matching on strings fails; matching on a spreadsheet category works only if both sides drew the category boundaries the same way, which nobody checks.

**Mapping.** A maintenance export has a tag column and a serial column side by side. An import script maps the tag to the physical item. Everything loads. Months later the history of the slot and the history of the machine are tangled together, and a blade that moved turbines carries the first turbine's failures with it.

**Words.** "Function" means three different things across these systems: what a part is physically able to do, the box it occupies in a functional diagram, and the job it happens to be doing right now. Mixing them up is the single most common modelling error in this space.

## Why not just pick the best standard?

Because there isn't a master. Each system is authoritative for its own question, and they disagree by design: the functional and product trees of the same designation standard don't even share parents. Converting everything into one of them throws away exactly the distinctions the others were built to keep.

Earlier efforts in other industries took the "master model" route — a reference library everyone maps into. That works when one party controls the reference. Wind energy has OEMs, operators, service companies, certifiers and researchers, each with their own systems and none with authority over the others.

## What WESO does instead

WESO is a **pivot**, not a master. It provides:

1. **Separate homes** for the things the systems conflate: the slot, the kind of slot, the physical item, the product specification, the space, the function, and the time a given item spent in a given slot.
2. **A contract** each source system signs: "strings with this prefix name slots; strings from this register name physical items." The contract is data, so it can be checked.
3. **Its own counting key.** Statistics are grouped by WESO's *position kind* ("planet bearing position"), not by any source system's category. Foreign categories are attached afterwards, as labels on the output.
4. **Checks.** Because the homes are separate, mistakes become detectable: a tag mapped to a serial number, two units in one slot, a gearbox recorded in a blade position.

The result: any number of systems can be connected, each through its own contract, without any of them having to change and without any of them being in charge.

## Who it is for

- **Ontology developers** building wind energy domain or application ontologies who need a stable, BFO-aligned layer to build on.
- **Data engineers and software developers** integrating maintenance, SCADA, PLM and asset data, who need identifiers resolved correctly and want the mistakes caught automatically.
- **Reliability analysts** pooling failure data across turbines, fleets or operators, who need the denominators to be right.
- **Standards people** who want to see how their designation scheme relates to the others, formally.

## Design benchmark

One question has been used throughout to test whether the core is sufficient:

> *What was the failure rate of the main bearing position across this fleet, distinguishing original units from replacements, and what mass of steel did those replacements represent?*

WESO's core answers the first two parts from its own structure (see the [blade example](worked-examples.md)). The third needs a materials extension, for which the core provides the hooks.
