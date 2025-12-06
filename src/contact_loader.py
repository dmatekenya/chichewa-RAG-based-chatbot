"""
Contact Information Loader

This module loads contact information from the National Bank website
and prepares it for the RAG chatbot.
"""

from typing import List
from langchain_core.documents import Document
import re


# Contact information extracted from https://www.natbank.co.mw/contact-us
CONTACTS_DATA = """
# National Bank of Malawi - Contact Information

## Head Office Contacts

Call Centre: callcentre@natbankmw.com, Phone: 626
Digital Financial Services Division: digitalfs@natbankmw.com, Phone: (265) 111 820 622
Credit Management Division: cmanagement@natbankmw.com, Phone: (265) 111 820 622
Finance Division: finance@natbankmw.com, Phone: (265) 111 820 622
Head Office: chiefexec@natbankmw.com, Phone: (265) 111 820 622
Human Capital Division: hcd@natbankmw.com, Phone: (265) 111 820 622
Information Technology Division: infotech@natbankmw.com, Phone: (265) 111 820 622
Leadership Centre: mtc@natbankmw.com, Phone: (265) 111 838 200
Operations Division: operations@natbankmw.com, Phone: (265) 111 820 622
Retail Banking Division: retailbanking@natbankmw.com, Phone: (265) 111 820 622
Internal Audit and Risk Group: orisgroup@natbankmw.com, Phone: (265) 111 820 622
Marketing and Corporate Affairs: marketing@natbankmw.com, Phone: (265) 111 820 622
Treasury and Investment Banking: treasury@natbankmw.com, Phone: (265) 111 820 622
Corporate Banking Division: cibd@natbankmw.com, Phone: (265) 111 824 907
Client Coverage Division: clientcoverage@natbankmw.com, Phone: (265) 111 820 622

## Service Centres and Branches

Balaka Service Centre: balaka@natbankmw.com, Phone: (265) 111 552 222
Capital City Service Centre: capitalcity@natbankmw.com, Phone: (265) 111 770 322
Chichiri Service Centre: chichiri@natbankmw.com, Phone: (265) 111 810 900
Chichiri Shopping Mall: chichirimall@natbankmw.com, Phone: (265) 111 873 774
Chileka Airport: chileka@natbankmw.com, Phone: (265) 111 692 392
Chitipa Service Centre: chitipa@natbankmw.com, Phone: (265) 111 382 419
Customs Road Service Centre: customs@natbankmw.com, Phone: (265) 111 840 133
Dwangwa Service Centre: dwangwa@natbankmw.com, Phone: (265) 111 295 350
Henderson Street Service Centre: hendersonstreet@natbankmw.com, Phone: (265) 111 821 000
Kamuzu International Airport: kia@natbankmw.com, Phone: (265) 111 700 772
Kanengo Service Centre: kanengo@natbankmw.com, Phone: (265) 111 710 193
Karonga Service Centre: karonga@natbankmw.com, Phone: (265) 111 362 223
Kasungu Service Centre: kasungu@natbankmw.com, Phone: (265) 111 253 224
Lilongwe Service Centre: lilongwe@natbankmw.com, Phone: (265) 111 757 016
Liwonde Service Centre: liwonde@natbankmw.com, Phone: (265) 111 542 866
Mangochi Service Centre: mangochi@natbankmw.com, Phone: (265) 111 594 322
Mchinji Service Centre: mchinji@natbankmw.com, Phone: (265) 111 242 236
Mponela Service Centre: mponela@natbankmw.com, Phone: (265) 111 286 300
Mulanje Service Centre: mulanje@natbankmw.com, Phone: (265) 999 978 552 / (265) 885 917 341
Mwanza Service Centre: mwanza@natbankmw.com, Phone: (265) 111 432 696
Mzimba Service Centre: mzimba@natbankmw.com, Phone: (265) 111 342 245
Mzuzu Service Centre: mzuzu@natbankmw.com, Phone: (265) 111 312 554
Nchalo Service Centre: nchalo@natbankmw.com, Phone: (265) 111 428 252
Ntcheu Service Centre: ntcheu@natbankmw.com, Phone: (265) 111 235 780
Songwe Agency: songwe@natbankmw.com, Phone: (265) 111 369 322
Salima Service Centre: salima@natbankmw.com, Phone: (265) 111 262 811
South End Service Centre: southend@natbankmw.com, Phone: (265) 887 378 400 / (265) 887 378 401
Thyolo Service Centre: thyolo@natbankmw.com, Phone: (265) 111 473 234
Victoria Avenue Service Centre: vicavenue@natbankmw.com, Phone: (265) 111 820 199
Zomba Service Centre: zomba@natbankmw.com, Phone: (265) 111 524 788
Lilongwe Gateway: lilongwegateway@natbankmw.com, Phone: (265) 111 762 954
Top Mandala: topmandala@natbankmw.com, Phone: (265) 111 820 950

## General Contact Information

For comments and feedback: clientcoverage@natbankmw.com
Call Centre: 626 (short code)
Main Head Office Line: (265) 111 820 622

Website: https://www.natbank.co.mw/contact-us
"""


def load_contacts_as_document() -> List[Document]:
    """
    Load contact information as LangChain documents
    
    Returns:
        List containing a single Document with all contact info
    """
    doc = Document(
        page_content=CONTACTS_DATA,
        metadata={
            "source": "National Bank Contact Information",
            "file_path": "https://www.natbank.co.mw/contact-us",
            "file_type": "contacts",
            "category": "contact_information"
        }
    )
    
    return [doc]


def get_contact_info() -> str:
    """
    Get the raw contact information text
    
    Returns:
        Contact information as string
    """
    return CONTACTS_DATA


if __name__ == "__main__":
    # Test the loader
    contacts = load_contacts_as_document()
    print(f"Loaded {len(contacts)} contact document(s)")
    print(f"\nMetadata: {contacts[0].metadata}")
    print(f"\nContent preview:\n{contacts[0].page_content[:500]}...")
