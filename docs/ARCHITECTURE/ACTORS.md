# Actor Architecture

Actors own business domains.

Agents specialize inside actors.

Workers perform mechanical operations for actors and flows.

## Actor boundary law

If a responsibility already has an owner, route work to that owner.

Never place code in an actor because it is convenient.

Ask:

Who owns this responsibility?

## Examples

- Packet Pilot owns paperwork.
- Legal Logger owns official reports.
- Error Echo owns active recovery.
- Big Bear owns root-cause investigation after recovery.
- Secret Safe owns protected secrets.
- Key Keeper owns authorization.
- Memory Mark owns unsafe memory validation.
- Direct Dispatch owns routing.
- CoDriver owns user interaction.

## Runtime relationship

Actor Runtime starts, stops, monitors, and invokes actors.

Actor Runtime does not own actor business meaning.
