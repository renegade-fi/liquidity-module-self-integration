# Pull Request Template: GlueX Liquidity Module Integration

## Protocol Information  
- **Protocol Name:** [Your Protocol Name]  
- **Protocol Website:** [Link to website or documentation]  
- **Indexing Smart Contract Addresses (e.g. factories):**  
  - [Chain 1]: 
    - [Contract Addresses, Contract Type]  
  - [Chain 2]: [Contract Addresses]  
    - [Contract Addresses, Contract Type]  
  - ...  

---

## Summary of Integration  
Provide a brief overview of your integration:  
- What does your protocol do?  
- What type of liquidity does it provide (DEX, lending, yield farming, etc.)?  
- Any unique features that GlueX should consider?  

---

## Implementation Details  
### Functions Implemented  
- `get_amount_out()`: [Brief explanation of how you retrieve output amounts]  
- `get_amount_in()`: [Brief explanation of how you determine input requirements]  
- `get_apy()`: [Brief explanation of APY calculation logic]  
- `get_tvl()`: [Brief explanation of TVL calculation logic]  

### Dependencies  
List any external dependencies (APIs, data sources, libraries). If none, state **N/A**.  

---

## Test Results  
Provide details of tests performed, including:  
- Test logs (paste relevant results)  
- Edge cases considered  
- Pass/fail outcomes  