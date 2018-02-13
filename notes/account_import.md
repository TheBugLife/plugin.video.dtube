Steps to import Steem wallet / account:

1. Install SteemPy library (Currently Python 3.6 -- but a branch has 2.7 support under development).
2. set steem 'nodes' via "steempy set nodes https://linktonodes" (see link at bottom for example)
3. Import account via:
 3.1 steempy importaccount accountnamehere
 3.2 input master password
 3.3 Active Key Import
 3.4 Set Passphrase
 3.5 Confirm Passphrase
 3.6 Posting / Memo Key import

4. Set system default account and vote weight (this could be used to switch between @mstafford / @jkms / @caitycat?)
 4.1 steempy set default_account accountnamehere
 4.2 steempy set default_vote_weight INT (integer between 0 & 100)

5. Verify Setup with "steempy config" in terminal.

## Steps graciously taken from article here:
## https://steemit.com/utopian-io/@steempytutorials/part-1-how-to-configure-the-steempy-cli-wallet-and-upvote-an-article-with-steem-python


