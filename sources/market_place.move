module sender::Marketplace {

    use std::signer;
    use std::vector;
    use std::coin;
    use std::string;
    use aptos_framework::coin::{Coin};

    struct Listing has key {
        seller: address,
        price: u64,
        item: string::String,
    }

    struct Listings has key {
        listings: vector<Listing>,
    }

    public fun initialize(account: &signer) {
        move_to(account, Listings {
            listings: vector::empty<Listing>(),
        });
    }

    public entry fun list_item(account: &signer, item: string::String, price: u64) {
        let address = signer::address_of(account);
        let listing = Listing { seller: address, price, item };
        let listings_ref = borrow_global_mut<Listings>(address);
        vector::push_back(&mut listings_ref.listings, listing);
    }

    public entry fun buy_item(account: &signer, seller: address, index: u64, payment: Coin) acquires Listings {
        let listings_ref = borrow_global_mut<Listings>(seller);
        let listing = vector::borrow(&listings_ref.listings, index);
        assert!(listing.price == coin::value(&payment), b"Incorrect payment");

        // Transfer funds to the seller
        coin::transfer(account, listing.seller, payment);

        // Remove the listing
        vector::swap_remove(&mut listings_ref.listings, index);
    }

    public fun get_listings(account: address): vector<Listing> acquires Listings {
        let listings_ref = borrow_global<Listings>(account);
        vector::clone(&listings_ref.listings)
    }
}