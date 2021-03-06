import React from "react"
import RegisterTable from "./RegisterTable/RegisterTable"

class Register extends React.Component{
    componentDidMount() {
        this.loadProjects()
    }
    state = {
        projects:{},
        select_project: {},
        visible: false
    }
    onChangeName=(e)=>{
        console.log(e.target)
        console.log(e.target.value)
        let a  = {...this.state.select_project}
        a.fields.name = e.target.value
        this.setState({select_project:a})
    }
    loadProjects = async () =>{
        let token = localStorage.getItem('token')
        let myHeaders = new Headers();
        myHeaders.append("Authorization", token);
        let requestOptions = {
            method: 'GET',
            headers: myHeaders,
            redirect: 'follow'
        };
        await fetch("http://127.0.0.1:8000/cabinet/projects/", requestOptions)
            .then(response => response.json())
            .then(result => this.setState({projects:result}))
        console.log('state',this.state)
    }

    onClickNewProject = () =>{
        document.location='/cabinet/admin/new_project'
    }
    onClickBack= () =>{
        document.location='/cabinet/admin/register'
        localStorage.setItem('selectProject','')
    }
    onClickEdit= (pk) =>{
        document.location='/cabinet/admin/edit_register'
        localStorage.setItem('selectProject',pk)
    }
    render(){
        console.log(this.state)
        return(
            <div className="container-fluid">
                <div className="row">
                    <div className="col-md-12">
                        <h3 className="text-left">Реестр проектов</h3>
                        <div className="buttons text-left">
                            <button type="button" className="btn btn-success btn-sm" onClick={this.onClickNewProject}>Добавить новый</button>
                                <button type="button" className="btn btn-primary btn-sm" style={{marginLeft:"5px"}}>Экспорт результатов</button>
                        </div>
                        <hr className="normal"/>

                        <RegisterTable
                            onClickEdit = {this.onClickEdit}
                            projects = {this.state.projects}/>

                    </div>
                </div>

            </div>
        )
    }
}

export default Register