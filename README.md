# **PawfectMatch API**

The PawfectMatch API is a Django API for [PawfectMatch](https://github.com/Julia-Wagner/PawfectMatch), a platform to connect shelters with loving homes for their dogs. Shelters can register and post their dogs, share stories and photos. Future dog owners can register to look for dogs.

# **Table of Contents**

<!-- TOC -->
* [**PawfectMatch API**](#pawfectmatch-api)
* [**Table of Contents**](#table-of-contents)
* [**Planning**](#planning)
  * [**User Stories**](#user-stories)
    * [**Epic: User Authentication**](#epic-user-authentication)
    * [**Epic: General UX**](#epic-general-ux)
    * [**Epic: Profile**](#epic-profile)
    * [**Epic: User Interaction**](#epic-user-interaction)
    * [**Epic: Posts**](#epic-posts)
    * [**Epic: Dog Posts**](#epic-dog-posts)
    * [**Epic: Notifications and Communication**](#epic-notifications-and-communication)
<!-- TOC -->

# **Planning**

I detailed planning process using the 5 UX planes is described in the [PawfectMatch repository](https://github.com/Julia-Wagner/PawfectMatch?tab=readme-ov-file#planning).

## **User Stories**

I created separate user stories for the API from the user stories defined for the frontend part of the project using the same epics to group them.

I also decided to add these stories to the project board in the main repo instead of creating a separate backend project. This way the entire development process is visible in one board.

### **Epic: User Authentication**

| User Story                                                                                                                                                          | Priority       |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| As a **developer**, I want to **access an API endpoint for registration**, so that I can **create users and profiles**.                                             | **MUST HAVE**  |
| As a **developer**, I want to **access an API endpoint for login**, so that I can **authenticate users**.                                                           | **MUST HAVE**  |
| As a **developer**, I want to **access an API endpoint for the feed without providing a logged-in user**, so that I can **access the feed without authentication**. | **MUST HAVE**  |

### **Epic: General UX**

| User Story                                                                                                                                                            | Priority      |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| As a **developer**, I want to **get appropriate error messages from the API in response to failed requests**, so that I can **provide users with detailed feedback**. | **MUST HAVE** |

### **Epic: Profile**

| User Story                                                                                                                          | Priority       |
|-------------------------------------------------------------------------------------------------------------------------------------|----------------|
| As a **developer**, I want to **perform CRUD operations for profiles**, so that I can **allow users to edit their profiles**.       | **MUST HAVE**  |
| As a **developer**, I want to **edit and get the profile status**, so that I can **show or hide profiles**.                         | **COULD HAVE** |

### **Epic: User Interaction**

| User Story                                                                                                                         | Priority        |
|------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| As a **developer**, I want to **access follow API endpoints**, so that I can **allow users to follow each other**.                 | **SHOULD HAVE** |
| As a **developer**, I want to **perform CRUD operations for comments**, so that I can **allow users to add comments to profiles**. | **COULD HAVE**  |
| As a **developer**, I want to **define banned words**, so that I can **ensure appropriate comments**.                              | **COULD HAVE**  |

### **Epic: Posts**

| User Story                                                                                                                                 | Priority        |
|--------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| As a **developer**, I want to **perform CRUD operations for posts**, so that I can **allow users to post content**.                        | **MUST HAVE**   |
| As a **developer**, I want to **access an API endpoint for saving a post**, so that I can **provide the user with a list of saved posts**. | **SHOULD HAVE** |

### **Epic: Dog Posts**

| User Story                                                                                                                             | Priority        |
|----------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| As a **developer**, I want to **have a special type of post for dogs**, so that I can **distinguish dog posts from other posts**.      | **MUST HAVE**   |
| As a **developer**, I want to **define requirements for dogs**, so that I can **use them for filtering**.                              | **COULD HAVE**  |
| As a **developer**, I want to **mark a dog as adopted**, so that I can **correctly show posts**.                                       | **SHOULD HAVE** |
| As a **developer**, I want to **receive dogs from the API based on defined criteria**, so that I can **allow filtering and matching**. | **SHOULD HAVE** |

### **Epic: Notifications and Communication**

| User Story                                                                                                                       | Priority        |
|----------------------------------------------------------------------------------------------------------------------------------|-----------------|
| As a **developer**, I want to **receive notifications from the API**, so that I can **alert the user**.                          | **COULD HAVE**  |
| As a **developer**, I want to **perform CRUD operations for chat messages**, so that I can **allow users to exchange messages**. | **COULD HAVE**  |
