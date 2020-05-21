# Quasi-Key Tableaux

Given a weak composition, a sample _quasi-key_ tableau is produced, along with
some other information about the weak composistion.

## Usage

The core logic is found in the [qtk-server](qtk-server/) folder.
This application heavily relies on
[Google OR-Tools](https://developers.google.com/optimization), specifically
the [CP-SAT Solver](https://developers.google.com/optimization/cp/cp_solver).
View the [Dockerfile](qtk-server/Dockerfile) to see how to `pip install`
the necessary libraries.

### Screenshot
![An example quasi-key tableau](assets/pic.png)
