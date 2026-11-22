# Strategy Pattern — Report Generation System

## UML Class Diagram

```mermaid
classDiagram
    class ReportFormatStrategy {
        <<abstract>>
        +generate(data: list) str
        +extension() str
    }

    class PDFFormatStrategy
    class ExcelFormatStrategy
    class CSVFormatStrategy
    class JSONFormatStrategy
    class HTMLFormatStrategy

    class ReportGenerator {
        -data: list
        -strategy: ReportFormatStrategy
        +set_strategy(strategy)
        +generate_report() str
        +save_report(filename)
    }

    ReportFormatStrategy <|-- PDFFormatStrategy
    ReportFormatStrategy <|-- ExcelFormatStrategy
    ReportFormatStrategy <|-- CSVFormatStrategy
    ReportFormatStrategy <|-- JSONFormatStrategy
    ReportFormatStrategy <|-- HTMLFormatStrategy

    ReportGenerator o-- ReportFormatStrategy : uses
