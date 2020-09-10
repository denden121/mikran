import React from "react"
import { Collapse, Button, Modal } from 'antd';
import CollapseList from "./CollapseList/CollapseList"
import ReportsTable from "./ReportsTable/ReportsTable"
import ReportModal from "./ReportModal/ReportModal"


class ListReports extends React.Component {
  
    state = {
        departments:[],
        select_department:'',
        subdepartments:[],
        select_subdepartments:'',
        reports:[],
        visible: false 
    }

    showModal = () => {
        this.setState({
          visible: true,
        });
      };
    
      handleOk = e => {
        console.log(e);
        this.setState({
          visible: false
        });
      };
    componentDidMount() {
        this.loadDepartments();
    }
    loadDepartments=()=>{
        let token = localStorage.getItem('token')
        let myHeaders = new Headers()
        myHeaders.append("Authorization", token)
        let requestOptions = {
            method: 'GET',
            headers: myHeaders,
            redirect: 'follow'
        }
        fetch("http://127.0.0.1:8000/departments/simple/", requestOptions)
            .then(response =>  response.json())
            .then(result => {
                let actions = Array.from(result).map((department)=>{
                    // console.log(department)
                    return {value:`${department.pk}`,label:`${department.fields.code +' '+ department.fields.name}`}
                })
                this.setState({departments: actions})})
            .catch(error => console.log('error', error))
    }
    onChangeSelectDepartments=(e)=>{
        let token = localStorage.getItem('token')
        let myHeaders = new Headers()
        myHeaders.append("Authorization", token)
        const date = localStorage.getItem('date').replace(' ','-')
        console.log(date)
        let requestOptions = {
            method: 'GET',
            headers: myHeaders,
            redirect: 'follow'
        }
        fetch(`http://127.0.0.1:8000/departments/${e}/subdepartments/`, requestOptions)
            .then(response =>  response.json())
            .then(result => {
                console.log('sub',result)
                let subdepartments = Array.from(result).map((subdepartment)=>{
                    // console.log(subdepartment)
                    return {value:`${subdepartment.pk}`,label:`${subdepartment.fields.code +' '+ subdepartment.fields.name}`}
                })
                this.setState({subdepartments: subdepartments})})
            .catch(error => console.log('error', error))

        fetch(`http://127.0.0.1:8000/reports/department/${e}/?date=${date}`, requestOptions)
            .then(response =>  response.json())
            .then(result => {
                console.log(result)
                this.setState({reports: result})
            })
            .catch(error => console.log('error', error))

    }
    render(){
        const { Panel } = Collapse;
        function callback(key) {
            console.log(key);
        }
        return(
            <div className="container-fluid">
                <div className="row">
                    <div className="col-lg-12">
                    <h3 className="text-left">Список отчетов</h3>
                    <hr/>
                    <Collapse accordion defaultActiveKey={['1']} onChange={callback}>
                    <Panel header="Параметры отображения" className="text-left" key="1">
                        <CollapseList
                            onChangeSelectDepartments = {this.onChangeSelectDepartments}    
                            departments = {this.state.departments}
                            subdepartments = {this.state.subdepartments}/>
                    </Panel>
                    </Collapse>    
                    </div>
                </div>
                <br/>
                <div className="row">
                    <div className="col-lg-12 text-left">
                        <Button>Импортировать отчеты</Button>
                    </div>
                </div>
                <br/>
                <div className="row">
                    <div className="col-lg-12">
<<<<<<< HEAD
                        <ReportsTable
                        reports = {this.state.reports}/>
=======
                        <ReportsTable onClickShowModal={this.showModal}/>
                        <Modal
                            title="Название дата"
                            visible={this.state.visible}
                            onOk={this.handleOk}
                            width={720}                            
                            okText="Блокировать"                                                    
                        >
                            <ReportModal/>
                        </Modal>
>>>>>>> fac90ba8a4ef1038beaf8af880a05f85790537fa
                    </div>
                </div>
            </div>
        )
    }
}

export default ListReports