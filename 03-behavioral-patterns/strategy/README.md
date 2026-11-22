# Strategy Pattern — Report Generation System

## Problem

The original ReportGenerator used long if/elif chains to handle PDF,
Excel, CSV and JSON reports.

This violated the Open/Closed Principle and made adding new formats
difficult.

## Solution

The Strategy Pattern separates formatting behavior from the context.

- ReportFormatStrategy: abstract interface
- PDFFormatStrategy: PDF-style report
- ExcelFormatStrategy: Excel-style report
- CSVFormatStrategy: CSV report
- JSONFormatStrategy: JSON report
- HTMLFormatStrategy: additional format
- ReportGenerator: context that delegates to the selected strategy

The UML class diagram is available in [uml.md](uml.md).

## Benefits

- No format-specific if/elif chains
- Each format is independently implemented and tested
- Strategies can be switched at runtime
- New formats can be added without modifying existing strategies
- Follows the Open/Closed Principle

## Running the demonstration

From the repository root:

    python3 -B 03-behavioral-patterns/strategy/report_strategy.py

## Running the tests

From the Strategy directory:

    python3 -B -m unittest -v

## Note

The PDF and Excel implementations reproduce the original exercise's
text-based simulations. They do not generate actual binary PDF or
XLSX files.
