# AnteciPay — Stage Details

## Stage 0: Prospecting

**Goal**: Make first contact, qualify basic interest  
**Agent**: cadence-antecipay (WhatsApp)  
**Duration**: 1-3 messages

### Flow
1. Send opener message (template)
2. Wait for response
3. If interested → ask qualifying questions:
   - "Você possui um precatório federal, estadual ou municipal?"
   - "Qual o valor aproximado?"
4. If qualified → advance to Stage 1

### Messages
See: `templates/messages/stage0_opener.md`

---

## Stage 1: Data Collection

**Goal**: Collect complete precatorio data  
**Agent**: cadence-antecipay  
**Duration**: 1-5 messages

### Data Collected
- Full name
- CPF (Brazilian tax ID)
- Precatorio process number
- Issuing tribunal (court)
- Precatorio type (federal/state/municipal)
- Approximate value
- Any pending legal issues

### Messages
See: `templates/messages/stage1_qualifier.md`

---

## Stage 2: Proposal

**Goal**: Analyze viability, generate and present proposal  
**Agent**: cadence-antecipay + PDF engine  
**Duration**: Same day turnaround

### Flow
1. Validate precatorio data (browser research if needed)
2. Calculate offer (value × rate)
3. Generate PDF proposal
4. Send PDF via WhatsApp
5. Explain terms verbally via WhatsApp
6. Handle objections

### Typical Rates
- Federal precatórios: 70-80% of face value
- State: 65-75%
- Municipal: 60-70%

---

## Stage 3: Closing

**Goal**: Formalize the deal, collect documents, transfer funds  
**Agent**: Human (backoffice) + agent support  
**Duration**: 3-7 business days

### Documents Required
- RG + CPF (identity)
- Comprovante de residência (address proof)
- Extrato bancário (bank statement)
- Certidão do precatório (official certificate)
- Procuração (power of attorney, if applicable)

### Flow
1. Agent collects documents via WhatsApp
2. Backoffice reviews and validates
3. Lawyer prepares cessão contract
4. Parties sign (electronic signature)
5. AnteciPay transfers agreed amount
6. Registration of cessão at tribunal
