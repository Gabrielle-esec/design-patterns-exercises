# Template Method Pattern — Data ETL Pipeline

## UML Class Diagram

```mermaid
classDiagram
    class DataPipeline {
        <<abstract>>
        +source: str
        +data: list
        +run() str
        +connect()*
        +extract()*
        +transform()*
        +validate()
        +load()
        +cleanup()
        +before_load()
    }

    class CSVPipeline
    class APIPipeline
    class DatabasePipeline
    class XMLPipeline

    DataPipeline <|-- CSVPipeline
    DataPipeline <|-- APIPipeline
    DataPipeline <|-- DatabasePipeline
    DataPipeline <|-- XMLPipeline

```

## Design Explanation

The run() method defines the fixed ETL workflow.
Concrete pipelines implement source-specific steps.
Validation and cleanup are shared across pipelines.
The before_load() method is an optional hook.
