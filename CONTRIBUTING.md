# CONTRIBUTING

## Afrixlabs Crypto Wallet Team

The following policy is a guideline to propose new data items and maintain existing items with outdated information:

1. A codebase is considered as `high quality` when one or more of the following criteria are met:
    * Contributing valuable knowledge for a specific codebase;
    * No advertisement! No Spam! No reputation promotion!

2. A new pull request will be merged into the core repository after passing automatic validation and maintainer's review.

3. An existing codebase item with outdated information (e.g., unavailable endpoint or features) will be removed after a while without new update.

## How to contribute a new data entry

It is simple to contribute to Afrixlab Crypto Wallet Backend (ACWB):

1. Fork `afrixlab_crypto_wallet_backend` repository into your own namespace such as `yourusername/afrixlab_crypto_wallet_backend`.

2. Clone your project locally:
```bash
git clone https://github.com/your_username/afrixlab_crypto_wallet_backend.git
cd afrixlab_crypto_wallet_backend
```

3. Create and activate your virtual environment

4. Run and install project dependencies since on local pc:
```bash
# With python
pip install -r requirements/local.txt
```
5. Create your env files and add to path 

6. Run the app migration to see status
``` bash
python3 manage.py migrate
```

7. Start the app on your local server
``` bash
python3 manage.py runserver
```

8. Work on your task or your contribution.

6. Commit local modifications to your repository:
```bash
git add .
git commit -m "Explain every details of what you worked on"  # Any message as you want
git push origin master
```

8. Create a new Pull Request to the trunk repository on Github page, usually `https://github.com/afrixlab/afrixlab_crypto_wallet_backend/pulls`