# saigen - dash config generator for SAI objects
* Based on `dashgen` modules
* Uses inheritance, reuses most methods
* Mostly just override renderItem() method to transform `dashgen` data structures into `SAI` structures prior to JSON seialization
* Initially showcase `eni` and `aclgroups` to demonstrate techniques.