from pydantic import BaseModel
from typing import List, Optional, Dict, Union

class UserPreference(BaseModel):
    name: str
    location: str
    interests: List[str]
    goal: str

class CustomerInput(BaseModel):
    cif: str
    acc_no: str
    segment: str
    name: str
    email: str
    products: List[str]
    fd_amt: float
    maturity_date: str
    balance: float
    int_rate: float
    proposed_rate: float
    balance_history: Dict[str, int]
    employer: str
    industry: str
    net_worth: float
    recent_activity: str
    campaign_history: str
    history: Dict[str, List[str]]
    transactions: List[Dict[str, Union[str, float]]]
    
class RMDecision(BaseModel):
    message: str
    suggested_action: str