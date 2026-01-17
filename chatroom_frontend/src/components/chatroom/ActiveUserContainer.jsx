import "./ActiveUserContainer.css";

export function ActiveUserContainer({users,currentUser}){

    return(
        <div className="ActiveUserContainer">
            <h3 className="OnlineUserListHeading">Online Users</h3>
            <ul className="UserList">
                {users.map((userId)=>(
                    <li 
                    key={userId}
                    className="UserListItem"
                    >
                        {userId} {userId === currentUser && "(You)"}
                    </li>
                ))}
                {users.length===0 && <p>Noone else is online</p>}
            </ul>
        </div>
    );
}