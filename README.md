# UniversalMarket
Masterthesis Delft University of Technology of Joost Verbraeken, MSc. Data Science

**Title thesis:** An explorative study for the design, implementation, and integration of a single universal globally distributed ledger to empower general-purpose peer-to-peer supply/demand-markets

### Description
To prevent a proliferation of many distributed ledgers (one to replace airbnb, one to replace amazon, one to replace banks, one to replace uber, etc.), I will develop a single universal distributed ledger.

Everything that can be traded is a product, which can be digital or physical. Products are identified by URNs and directly linked to the semantic web. For example, when an airbnb is in Delft, it is automatically also in South Holland, and in The Netherlands, because these geographical regions are semantically linked to each other. This enables the buyer to easily find the products he's looking for. However, there are so many (unnecessary) attributes that can theoretically be linked to a product that it can be daunting for the seller. Therefore, people can use Templates that are a collection of fields that are important for particular products. For example, when you would add a laptop to the system, you can search for a laptop template that contains field with i.a. the screen size and amount of memory.

2 problems and their respective solutions:

Problem: Keeping a track of all 100m+ products can be computationally quite demanding and undesirable from a user's point of view
Solution: only the product URN is placed on the trustchain. Entrepreneurs can host a Toogle service (Google for Transactions) that indexes all products and that can be used by the user to search for them. Setting up a new Toogle service should be easy to create lots of competition => drive price down and quality up
Problem: Because description of items can take up a lot of space (e.g. pictures and videos), it is (I presume - check this (!)) unreasonable to put these descriptions directly on the trustchain
Solution: the whole description (text, images, videos, sounds, etc.) is hosted by Tikipedia services (Wikipedia for Transactions), offered by entrepreneurs. Sellers can put their description on several Tikipedia services. Toogle service will crawl them and add a link to these descriptions (based on the product URNs) to their database. Again, setting up a Tikipedia service should be easy to create competition.
The user MUST be able to pay with dollars/euros and MUST be able to get things like a refund even when the seller disagrees, otherwise the system will not be used by the early/late majority. To do this, we will use "custodians". The user pays the custodian for the product + a small fee (whatever fee the custodian deems appropriate) and the custodian arranges for nice payment methods, great customer guarantees, excellent customer service, etc. Custodians can compete based on, for example, price and quality, and can also be reviewed by the customer.

There are several things I still have to look into which intuitively seems very hard to do properly, including an age check, Know Your Customer (KYC), Anti-Money Laundering (AML), Counter-Terrorism Financing (CTF), and creditworthiness checks.
