# KYBchain1

This is the POC implementation of KYBchain framework

Folder Structure

privacyratingExperiments: consists of all the simulations to analyze the usability of privacy rating

POC:

contracts: contains all the marketplace contracts (registerSc, subscriptionSc) and KYB module specific contracts (privacyRatingSc, ruleSc, buyerSc)

User.py: Class to define method and attricbutes for user profile in marketplace

admin.py: Class to define method and attricbutes for admin profile including auditor and regulator in marketplace

setup.py: deploys all the smart contracts in the network

Baseline: Contains the implementation of baseline (registerSc, subscriptionSc, )

caliper_benchmark: contains all the config files to run tests on the SUT. It is equipped with all the aforementioned contracts for benchmarking purpose.
