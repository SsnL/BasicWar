# Basic War

+ Explores AI player in the game Basic War.

## Rules

Basic War is a variant of the popular TCG, *Magic: the Gathering* (abbreviated as MTG). The rule is found on [a Chinese forum](http://www.iplaymtg.com/forum.php?mod=viewthread&tid=92319), translated to English as following:

+ There are five kinds of "basic land card" in MTG: *Mountain*, *Plains*, *Forest*, *Swamp* and *Islands*.

+ Two player each starts with a deck of 50 cards, composed of ten of each basic land.

+ Player shuffles their decks and each draw five cards.

+ Each player plays in his/her turn alternatively.

+ Terminologies:
    + Play a card
        + Put a card from your hand into an area called your "battlefield", facing upwards.
    + Discard a card
        + Put a card from your hand into an area called "graveyard", facing upwards.
    + Destroy target land
        + Put one land card on any player's battlefield into that player's graveyard.
        
+ During a turn, the current playing player 
    + must draw a card,
    + may play a card, and
    + discard cards until he/she has no more than seven cards in hand.
    
+ Each type of card has its own special abilities:
    + *Mountain*
        + When played, destroy target land.
    + *Plains*
        + When played, draw a card.
    + *Forest*
        + When played, put target card in your graveyard back to your hand.
    + *Swamp*
        + When played, your opponent discard a card.
    + *Islands*
        + When opponent plays a card, you may discard a same card **and** an *Islands*. If you do so, that card opponent plays has no effect and is put into opponent's graveyard.

+ A player wins the game when there is at least one of each type of land on his/her battlefield.

## Goals of this project

+ Develop an appropriate AI for this game.

+ Try and see if using NN and only NN can be a good AI in this rather simple game.