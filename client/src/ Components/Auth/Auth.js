import React from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import './Auth.css'
import picture from './micran1.png'

const Auth =(props)=>{
    return(
        <div className="container-fluid">
            <div className="form-signin">
                <img src={picture} alt="" className="img-fluid"></img>
                <div className="form-froup">
                    <label className="Label">Имя пользователя</label>
                    <input type="text" className="form-control form-control-lg" id="input-login"/>
                </div>

                <div className="form-froup">
                    <label className="Label">Пароль</label>
                    <input type="password" className="form-control form-control-lg" id="input-password"/>
                </div>

                {/*<div className="checkBox" align="left">*/}
                {/*    <label className="checkbox">*/}
                {/*        <input type="checkbox"/>*/}
                {/*        Запомнить меня*/}
                {/*    </label>*/}
                {/*</div>*/}
                <div className='error-label error-label-1'>Не правильный пароль или логин</div>
                <div className='error-label error-label-2'>Введите логин или пароль</div>
                <button onClick={props.authHandler} type="submit" className="btn btn-lg btn-primary">Войти</button>
            </div>
        </div>
    )
}

export default Auth;