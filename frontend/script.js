const API_URL = "http://localhost:5000";


// =================================
// ADD MEMBER
// =================================

async function addMember() {

    const name =
        document.getElementById("name").value;

    const age =
        document.getElementById("age").value;

    const gender =
        document.getElementById("gender").value;


    if (!name) {

        alert("Please enter the member name.");

        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/members`,
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    name: name,

                    age: age,

                    gender: gender

                })

            }
        );


        const data =
            await response.json();


        alert(
            data.message || data.error
        );


        document.getElementById("name").value = "";

        document.getElementById("age").value = "";

        document.getElementById("gender").value = "";


        loadMembers();

    }

    catch (error) {

        alert(
            "Cannot connect to Flask server."
        );

        console.error(error);

    }

}


// =================================
// LOAD MEMBERS
// =================================

async function loadMembers() {

    try {

        const response =
            await fetch(
                `${API_URL}/members`
            );


        const members =
            await response.json();


        const list =
            document.getElementById(
                "membersList"
            );


        list.innerHTML = "";


        const person1 =
            document.getElementById(
                "person1"
            );


        const person2 =
            document.getElementById(
                "person2"
            );


        const findPerson1 =
            document.getElementById(
                "findPerson1"
            );


        const findPerson2 =
            document.getElementById(
                "findPerson2"
            );


        person1.innerHTML =
            '<option value="">Select First Person</option>';


        person2.innerHTML =
            '<option value="">Select Second Person</option>';


        findPerson1.innerHTML =
            '<option value="">Select First Person</option>';


        findPerson2.innerHTML =
            '<option value="">Select Second Person</option>';


        members.forEach(member => {


            // Display member

            list.innerHTML += `

                <div class="member">

                    <strong>
                        ${member.name}
                    </strong>

                    <br>

                    Age:
                    ${member.age || "N/A"}

                    <br>

                    Gender:
                    ${member.gender || "N/A"}

                    <br>

                    <button
                        class="delete-button"
                        onclick="deleteMember('${member.id}')"
                    >
                        Delete
                    </button>

                </div>

            `;


            // Relationship dropdown

            person1.innerHTML += `

                <option value="${member.id}">
                    ${member.name}
                </option>

            `;


            person2.innerHTML += `

                <option value="${member.id}">
                    ${member.name}
                </option>

            `;


            // Find relationship dropdown

            findPerson1.innerHTML += `

                <option value="${member.id}">
                    ${member.name}
                </option>

            `;


            findPerson2.innerHTML += `

                <option value="${member.id}">
                    ${member.name}
                </option>

            `;

        });

    }

    catch (error) {

        console.error(error);

    }

}


// =================================
// DELETE MEMBER
// =================================

async function deleteMember(id) {


    const confirmDelete =
        confirm(
            "Are you sure you want to delete this member?"
        );


    if (!confirmDelete) {

        return;

    }


    try {

        const response =
            await fetch(
                `${API_URL}/members/${id}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        alert(
            data.message || data.error
        );


        loadMembers();

        loadRelationships();

    }

    catch (error) {

        alert(
            "Error deleting member."
        );

    }

}


// =================================
// ADD RELATIONSHIP
// =================================

async function addRelationship() {


    const person1_id =
        document.getElementById(
            "person1"
        ).value;


    const person2_id =
        document.getElementById(
            "person2"
        ).value;


    const relationship =
        document.getElementById(
            "relationship"
        ).value;


    if (
        !person1_id ||
        !person2_id ||
        !relationship
    ) {

        alert(
            "Please fill all relationship fields."
        );

        return;

    }


    if (person1_id === person2_id) {

        alert(
            "A person cannot be related to themselves."
        );

        return;

    }


    try {

        const response =
            await fetch(
                `${API_URL}/relationships`,
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        person1_id:
                            person1_id,

                        person2_id:
                            person2_id,

                        relationship:
                            relationship

                    })

                }
            );


        const data =
            await response.json();


        alert(
            data.message || data.error
        );


        loadRelationships();

    }

    catch (error) {

        alert(
            "Cannot connect to Flask server."
        );

    }

}


// =================================
// LOAD RELATIONSHIPS
// =================================

async function loadRelationships() {


    try {

        const response =
            await fetch(
                `${API_URL}/relationships`
            );


        const relationships =
            await response.json();


        const membersResponse =
            await fetch(
                `${API_URL}/members`
            );


        const members =
            await membersResponse.json();


        const list =
            document.getElementById(
                "relationshipsList"
            );


        list.innerHTML = "";


        relationships.forEach(
            relation => {


                const person1 =
                    members.find(
                        member =>
                            member.id ===
                            relation.person1_id
                    );


                const person2 =
                    members.find(
                        member =>
                            member.id ===
                            relation.person2_id
                    );


                list.innerHTML += `

                    <div class="relationship">

                        <strong>
                            ${
                                person1
                                ? person1.name
                                : "Unknown"
                            }
                        </strong>

                        →

                        <strong>
                            ${relation.relationship}
                        </strong>

                        →

                        <strong>
                            ${
                                person2
                                ? person2.name
                                : "Unknown"
                            }
                        </strong>

                    </div>

                `;

            }
        );

    }

    catch (error) {

        console.error(error);

    }

}


// =================================
// FIND RELATIONSHIP
// =================================

async function findRelationship() {


    const person1 =
        document.getElementById(
            "findPerson1"
        ).value;


    const person2 =
        document.getElementById(
            "findPerson2"
        ).value;


    const result =
        document.getElementById(
            "relationshipResult"
        );


    if (!person1 || !person2) {

        result.innerHTML =
            "Please select both persons.";

        return;

    }


    if (person1 === person2) {

        result.innerHTML =
            "Please select two different persons.";

        return;

    }


    try {

        const response =
            await fetch(
                `${API_URL}/relationship/${person1}/${person2}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            result.innerHTML =
                data.message;

            return;

        }


        result.innerHTML = `

            Relationship Path:

            <br><br>

            ${data.relationship}

        `;

    }

    catch (error) {

        result.innerHTML =
            "Cannot connect to Flask server.";

    }

}


// =================================
// LOAD DATA WHEN PAGE OPENS
// =================================

window.onload = function () {

    loadMembers();

    loadRelationships();

};
