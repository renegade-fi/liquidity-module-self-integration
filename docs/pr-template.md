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
### Execution Functions Required  
List all execution functions that GlueX needs to interact with your protocol, including:  
- Function names and descriptions  
- Input and output parameters  
- Relevant smart contract references  

### Functions Implemented  
- `get_amount_out()`: [Brief explanation of how you retrieve output amounts]  
- `get_amount_in()`: [Brief explanation of how you determine input requirements]  
- `get_apy()`: [Brief explanation of APY calculation logic]  
- `get_tvl()`: [Brief explanation of TVL calculation logic]  

### Dynamic States Required for AMM Calculations  
Specify any on-chain values that change frequently and are required for accurate AMM computations, such as:  
- Current reserves  
- Current prices  
- Pending liquidity changes  
- Other time-sensitive variables  

### Static States Required for AMM Calculations  
Specify any on-chain values that remain constant such as:  
- Fee tiers  
- Immutable contract parameters  
- Other relevant constants  

### Dependencies  
List any external dependencies (APIs, data sources, libraries). If none, state **N/A**.  

### Other Requirements  
- **API Keys:** If your integration requires API keys, provide details on how to obtain them.  
- **Special Access Requirements:** Any required permissions, whitelisting, or approvals.  

---

## Test Results  
Provide details of tests performed, including:  
- Test logs (paste relevant results)  
- Edge cases considered  
- Pass/fail outcomes  

