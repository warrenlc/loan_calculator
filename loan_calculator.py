#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 00:14:50 2021

@author: warrencrutcher
"""
import argparse
import math

# Add the arguments expected by the user from the Terminal
parser = argparse.ArgumentParser()             
parser.add_argument("--type", type=str)
parser.add_argument("--payment", type=float)
parser.add_argument("--principal", type=float)
parser.add_argument("--periods", type=float)
parser.add_argument("--interest", type=float)

args = parser.parse_args()

# a list of inputs (as opposed to Namespace) is nice for evaluating number of arguments and negative values
inputs = []
for arg in vars(args):
    if getattr(args, arg) is not None:
        inputs.append(getattr(args, arg))
       

def annuity_payment(p, i, n):  # Returns fixed monthly payment for the loan term
    annuity = p * ((i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1))
    return math.ceil(annuity)

def loan_principal(a, i, n):  # Returns the initial amount borrowed
    power = math.pow(1 + i, n)
    principal = a / ((i * power) / (power - 1))
    return math.floor(principal)

def number_payments(a, i, p):  # Returns the number of payments, or payment periods
    payments = math.log(a/(a - i * p), 1 + i)
    return math.ceil(payments)

def diff (p, i, n, m):         # Returns the monthly differentiated payment
    diff_payment = p / n + i * (p - ((p * (m - 1)) / (n)))
    return diff_payment


### Evaluate the arguments given by the user for validity ###
if args.type != "annuity" and args.type != "diff":
    print("Incorrect parameters--'type' must be either 'annuity' or 'diff'. ")
elif args.type == "diff" and args.payment != None:
    print("Incorrect parameters-- type 'diff' and no payment are incompatible. ")
elif args.interest == None:
    print("Incorrect parameters-- user must always provide an interest rate. ")
elif len(inputs) < 4:
    print("Incorrect parameters-- user must enter at least 4 arguments. ")
        
for i in inputs:
    if type(i) is not str and i < 0:
        print("Incorrect parameters-- Negative values not allowed. ")
            
# Proceed ONLY if the user gave an interest rate
if args.interest != None:  
    nominal_interest = float(args.interest / 1200)  # Always turn our INTEREST input into a usuable decimal value.

    if args.type == "diff":        # Print the differentiated payment for each month of the loan term
        total_payments = 0
        for k in range(1, (int(args.periods + 1))):
            payment = math.ceil(diff(args.principal, nominal_interest, args.periods, k))
            total_payments += payment
            print(f"Month {k}: payment is {payment} ")
        overpayment = total_payments - args.principal
        print()
        print(f"Overpayment = {int(overpayment)}")

    elif args.type == "annuity" and args.payment == None:  # Given the principal, but no payment, prints the fixed monthly payment
        payment = annuity_payment(args.principal, nominal_interest, args.periods)
        overpayment = payment * args.periods - args.principal
        print(f"Your annuity payment = {payment}!")
        print(f"Overpayment = {overpayment}")
    
    elif args.type == "annuity" and args.principal == None:  # Given the payment but no principal, prints the loan principal
        principal = loan_principal(args.payment, nominal_interest, args.periods)
        overpayment = args.payment * args.periods - principal
        print(f"Your loan principal = {principal}!")
        print(f"Overpayment = {int(overpayment)}")

    elif args.periods == None:   # Given the payment and principal, return how long it will take to repay the loan
        months = int(number_payments(args.payment, nominal_interest, args.principal))
        overpayment = args.payment * months - args.principal
        if months % 12 == 0:
            print(f"It will take {int(months // 12)} years to repay this loan! ")
        else:
            print(f"It will take {int(months // 12)} years and {int(months % 12)} months to repay this loan! ")
        print(f"Overpayment = {int(overpayment)}")
