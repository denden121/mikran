import React from "react";
import './Auth.css';

const Auth= (props)=>{
    return(
        < div className="classes.Auth">
            {/*<form >*/}
                <fieldset className="accountInfo">
                    <label>Имя пользователя
                         <input type="text" name="username"></input>
                    </label>
                    <label>Пароль
                         <input type="text"></input>
                    </label>
                </fieldset>
                <fieldset className="accountAction">
                     <button onClick={props.authHandler}>Войти</button>
                         <label>
                              <input type="checkbox" name="remember"/> Запомнить
                          </label>
                </fieldset>
            {/*<    /form>*/}
        </div>
    )
}
export default Auth;