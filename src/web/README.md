# Design

```mermaid
graph TD;
  React.js:WebUI-->GraphQL:API
  GraphQL:API-->API_1:TypeScript
  GraphQL:API-->API_2:Go
  API_1:TypeScript-->ImageBlob:Azure
```