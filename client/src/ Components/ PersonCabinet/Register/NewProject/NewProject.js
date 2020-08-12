import React from "react"
import "./NewProject.css"
import Register from "../Register"
import {Select} from "antd";
import makeAnimated from "react-select/animated/dist/react-select.esm";
import { Radio } from 'antd';
import { Checkbox } from 'antd';

class NewProject extends React.Component{
    state={
        people:{},
        directors:{},
        directions:{},
        select_direction:'',
        select_director:'',
        select_designer:'',
        select_deputy_designer:'',
        type:'',
        state_project:'',
        availability:'',
        vp:''
    }
    loadDate = async () =>{
        let myHeaders = new Headers();
        let token = localStorage.getItem('token')
        myHeaders.append("Authorization", token);
        let requestOptions = {
            method: 'GET',
            headers: myHeaders,
            redirect: 'follow'
        };
        let directionValue;
        let directorValue;
        let peopleValue;
        await fetch("http://127.0.0.1:8000/directions/", requestOptions)
            .then(response => response.json())
            .then(result =>{
                directionValue = Array.from(result)
                directionValue = directionValue.map(direction => {
                    return {value:`${direction.pk}`,label:`${direction.direction}`}
                })
                console.log(directionValue)
            } )
            .catch(error => console.log('error', error));
        await fetch("http://127.0.0.1:8000/workers/project/managers/", requestOptions)
            .then(response => response.json())
            .then(result =>{
                directorValue = Array.from(result)
                directorValue = directorValue.map(director => {
                    return {value:`${director.pk}`,label:`${director.fields.last_name + ' ' + director.fields.first_name+' '+director.fields.middle_name}`}
                })
            } )
            .catch(error => console.log('error', error))
        await fetch("http://127.0.0.1:8000/workers/project/", requestOptions)
            .then(response => response.json())
            .then(result =>{
                peopleValue = Array.from(result)
                peopleValue = peopleValue.map(director => {
                    return {value:`${director.pk}`,label:`${director.fields.last_name + ' ' + director.fields.first_name+' '+director.fields.middle_name}`}
                })
            })
            .catch(error => console.log('error', error));
        this.setState({
            people: peopleValue,
            directions: directionValue,
            directors:directorValue
        })
    }
    onChangeSelectDirection=(event)=>{
        this.setState({select_direction:event})
        // console.log(this.state)
    }
    onChangeSelectDirector=(event)=>{
        this.setState({select_director:event})
        // console.log(this.state)
    }
    onChangeSelectDesigner=(event)=>{
        this.setState({select_designer:event})
        // console.log(this.state)
    }
    onChangeSelectDeputyDesigner=(event)=>{

        this.setState({select_deputy_designer:event})
        // console.log(this.state)
    }
    onChangeType=(e)=>{
        this.setState({type:e.target.value})
    }

    onChangeState=(e)=>{
        this.setState({state_project:e.target.value})
    }

    onChangeAvailability=(e)=>{
        this.setState({availability:e.target.value})

    }
    onChangeVp=(e)=>{
        this.setState({vp:e.target.checked})
    }
    onClickCreateGroup=async ()=>{
        const direction = this.state.select_direction
        const director = this.state.select_director
        const disigner = this.state.select_designer
        const deputyDesigner = this.state.select_deputy_designer
        const state = this.state.state_project
        const type = this.state.type
        const availability = this.state.availability
        const vp = this.state.vp
        const nameproject = document.querySelector('#name-project-new-project').value
        const number = document.querySelector('#number-contract-new-project').value
        const order = document.querySelector('#order-new-project').value
        const productionOrder = document.querySelector('#production-order-new-project').value
        const comment = document.querySelector('#comment-to-co-workers-new-project').value
        console.log(direction,director,disigner,deputyDesigner,state,type,availability,vp,nameproject,number,order,productionOrder,comment)
        var myHeaders = new Headers();
        myHeaders.append("Authorization", );

        var formdata = new FormData();
        formdata.append("pk", "6");
        formdata.append("name", "hjgkslsjgkrgbjklt");
        formdata.append("actions", "1 2 ");
        formdata.append("participants", "1 2 ");

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: formdata,
            redirect: 'follow'
        };

        fetch("http://127.0.0.1:8000/admin/groups_admin/", requestOptions)
            .then(response => response.text())
            .then(result => console.log(result))
            .catch(error => console.log('error', error));
    }
    componentDidMount() {
        this.loadDate()
    }

    render() {
        const animatedComponents = makeAnimated();
        // console.log(this.state)
        return (
            <div className="container-fluid">
                <div className="row">
                    <div className="col-lg-12">
                        <h3 className="text-left">Новый проект</h3>
                        <div
                            className="row no-gutters border rounded overflow-hidden flex-lg-row mb-4 shadow-sm h-lg-250 position-relative">
                            <div className="col p-4 d-flex flex-column position-static">
                                <div className="block1">
                                    <div className="input-group mb-3 input-group-lg">
                                        <label className="napr col-sm-2 text-left"
                                               style={{fontSize: "16px"}}>Направления</label>
                                        <Select
                                            onChange = {this.onChangeSelectDirection}
                                            closeMenuOnSelect={true}
                                            components={animatedComponents}
                                            options={this.state.directions.length ? this.state.directions :''}
                                            placeholder="Выбрать"
                                        />
                                    </div>
                                    <br/>
                                    <div className="input-group mb-3 input-group-sm">
                                        <label className="napr col-sm-2 text-left" style={{fontSize: "16px"}}>Новый
                                            проект</label>
                                        <textarea
                                            id={'name-project-new-project'}
                                            className="form-control"
                                            rows="2"
                                            placeholder="Новый проект">
                                    </textarea>
                                    </div>
                                    <hr className="normal"/>
                                </div>
                                <div className="block2">
                                    <div className="input-group mb-3 input-group-sm">
                                        <label className="napr col-sm-2 text-left"
                                               style={{fontSize: "16px"}}>Руководитель</label>
                                        <Select
                                            onChange = {this.onChangeSelectDirector}
                                            closeMenuOnSelect={true}
                                            components={animatedComponents}
                                            options={this.state.directors.length ? this.state.directors :''}
                                            placeholder="Выбрать"
                                        />
                                    </div>
                                    <div className="input-group mb-3 input-group-sm">
                                        <label className="napr col-sm-2 text-left" style={{fontSize: "16px"}}>Главный
                                            конструктор</label>
                                        <Select
                                            onChange = {this.onChangeSelectDesigner}
                                            closeMenuOnSelect={true}
                                            components={animatedComponents}
                                            options={this.state.directors.length ? this.state.directors :''}
                                            placeholder="Выбрать"
                                        />
                                    </div>
                                    <div className="input-group mb-3 input-group-sm">
                                        <label className="napr col-sm-2 text-left" style={{fontSize: "16px"}}>Зам.главного
                                            конструктора</label>
                                        <Select
                                            onChange = {this.onChangeSelectDeputyDesigner}
                                            closeMenuOnSelect={true}
                                            components={animatedComponents}
                                            options={this.state.people.length ? this.state.people :''}
                                            placeholder="Выбрать"
                                            width = {'700pxgit '}
                                        />
                                    </div>
                                    <hr className="normal"/>
                                </div>
                                <div className="block3">
                                    <div className="input-group mb-3 input-group-sm">
                                        <label className="napr col-sm-2 text-left" style={{fontSize: "16px"}}>№
                                            договора</label>
                                        <textarea
                                            id={'number-contract-new-project'}
                                            className="form-control"
                                            rows="2"
                                            placeholder="№ договора">
                                </textarea>
                                    </div>
                                    <div className="input-group mb-3 input-group-sm">
                                        <label className="napr col-sm-2 text-left"
                                               style={{fontSize: "16px"}}>Заказчик</label>
                                        <textarea
                                            id={'order-new-project'}
                                            className="form-control"
                                            rows="2"
                                            placeholder="Заказчик">
                                    </textarea>
                                    </div>
                                    <div className="input-group mb-3 input-group-sm">
                                        <label className="napr col-sm-2 text-left" style={{fontSize: "16px"}}>Заказ на
                                            производство</label>
                                        <textarea
                                            id={'production-order-new-project'}
                                            className="form-control"
                                            rows="2"
                                            placeholder="Заказ на производство">
                                    </textarea>
                                    </div>
                                    <div className="input-group mb-3 input-group-sm">
                                        <label className="napr col-sm-2 text-left" style={{fontSize: "16px"}}>Комментарий
                                            для сотрудников</label>
                                        <textarea
                                            id={'comment-to-co-workers-new-project'}
                                            className="form-control"
                                            rows="2"
                                            placeholder="Описание">
                                    </textarea>
                                    </div>
                                    <div>
                                        <div className="input-group mb-3 input-group-sm">
                                            <label className="napr col-sm-2 text-left"
                                                   style={{fontSize: "16px"}}>Тип</label>
                                            <div className="checkbox checkbox-inline ">
                                                <Radio.Group  onChange={this.onChangeType}>
                                                    <Radio value={0}><label for="inlineCheckbox1" style={{
                                                        border: "3px solid grey",
                                                        background: "grey",
                                                        color: "white",
                                                        borderRadius: "7px",
                                                        fontSize: "12px",
                                                        marginLeft: "5px"
                                                    }}> Внутр</label></Radio>
                                                    <Radio value={1}><label for="inlineCheckbox1" style={{
                                                        border: "3px solid #FF7A36",
                                                        background: "#FF7A36",
                                                        color: "white",
                                                        borderRadius: "7px",
                                                        fontSize: "12px",
                                                        marginLeft: "5px"
                                                    }}>Внеш</label></Radio>
                                                </Radio.Group>

                                            </div>
                                        </div>
                                        <div className="input-group mb-3 input-group-sm">
                                            <label className="napr col-sm-2 text-left"
                                                   style={{fontSize: "16px"}}>Состояние</label>
                                            <div className="checkbox checkbox-inline ">
                                                <Radio.Group onChange={this.onChangeState}>
                                                    <Radio value={0}><label for="inlineCheckbox1" style={{
                                                        border: "3px solid #6FD76F",
                                                        background: "#6FD76F",
                                                        color: "white",
                                                        borderRadius: "7px",
                                                        fontSize: "12px",
                                                        marginLeft: "5px"
                                                    }}>Открыт</label></Radio>
                                                    <Radio value={1}><label for="inlineCheckbox1" style={{
                                                        border: "3px solid #E23C3C",
                                                        background: "#E23C3C",
                                                        color: "white",
                                                        borderRadius: "7px",
                                                        fontSize: "12px",
                                                        marginLeft: "5px"
                                                    }}>Закрыт</label></Radio>
                                                </Radio.Group>
                                            </div>
                                        </div>
                                        <div className="input-group mb-3 input-group-sm">
                                            <label className="napr col-sm-2 text-left" style={{fontSize: "16px"}}>Доступность
                                                для отчетов сотрудников</label>
                                            <div className="checkbox checkbox-inline ">
                                                <Radio.Group onChange={this.onChangeAvailability}>
                                                    <Radio value={0}><label for="inlineCheckbox1" style={{
                                                        border: "3px solid #6FD76F",
                                                        background: "#6FD76F",
                                                        color: "white",
                                                        borderRadius: "7px",
                                                        fontSize: "12px",
                                                        marginLeft: "5px"
                                                    }}>Досупен</label></Radio>
                                                    <Radio value={1}><label for="inlineCheckbox1" style={{
                                                        border: "3px solid #E23C3C",
                                                        background: "#E23C3C",
                                                        color: "white",
                                                        borderRadius: "7px",
                                                        fontSize: "12px",
                                                        marginLeft: "5px"
                                                    }}>Недоступен</label></Radio>
                                                </Radio.Group>
                                            </div>
                                        </div>
                                        <div className="input-group mb-3 input-group-sm">
                                            <label className="napr col-sm-2 text-left" style={{fontSize: "16px"}}>Приемка
                                                ВП</label>
                                            <div className="checkbox checkbox-inline ">
                                                <Checkbox onChange={this.onChangeVp}>
                                                    <label for="inlineCheckbox1" style={{
                                                    border: "3px solid #454545",
                                                    background: "#454545",
                                                    color: "white",
                                                    borderRadius: "7px",
                                                    fontSize: "12px",
                                                    marginLeft: "5px"
                                                    }}>ПП</label>
                                                </Checkbox>
                                            </div>
                                        </div>
                                    </div>
                                    <hr className="normal"/>
                                </div>
                                <div className="block4 text-right">
                                    {/* <button type="button" className="btn btn-primary btn-sm" onClick={()=>document.location='/cabinet/admin/register'}>Назад</button> */}
                                    <button onClick={this.onClickCreateGroup} type="button" className="btn btn-success btn-sm"
                                            style={{marginLeft: "5px"}}>Сохранить
                                    </button>
                                    <button type="button" className="btn btn-secondary btn-sm"
                                            style={{marginLeft: "5px"}}
                                            onClick={() => document.location = '/cabinet/admin/register'}>Отмена
                                    </button>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default NewProject