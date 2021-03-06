import React, {Component} from "react"
import 'bootstrap/dist/css/bootstrap.min.css';
// import Header from "../Header/Header"
import LogOut from "../Header/Header"
import SendReport from "../SendReport/SendReport"
// import rend from '../../../index.js'
import PersonData from "../PersonData/PersonData";
import moment from 'moment';
import "./Main.css"
import Switch from "react-bootstrap/cjs/Switch";
import {Redirect, Route} from "react-router-dom";
import ManageGroupps from "../Administration/ManageGroups/ManageGroupps";
import ViewLogs from "../Administration/ViewLogs/ViewLogs";
import Salary from "../Salary/Salary"
import rend from "../../../index";
import Payroll from "../Payroll/Payroll"
import Register from "../Register/Register"
import NewProject from "../Register/NewProject/NewProject";
import UnitProjects from "../Register/UnitProjects/UnitProjects"
import Employees from "../Employees/Employees"
import Interval from "../WorkCalendar/Interval/Interval"
import AddGroups from "../Administration/AddGroups/AddGroups"
import SystemTime from "../SystemTime/SystemTime"
import Structure from "../Tree/Structure"
import ListReports from "../ListReports/ListReports"
import { DatePicker, Space } from 'antd';
import { Layout, Menu, PageHeader,Button} from 'antd';
import EditGroupps from "../Administration/AddGroups/EditGroupps/EditGroupps"
import { UpSquareOutlined,TeamOutlined,UsergroupAddOutlined } from '@ant-design/icons';
import {
    DesktopOutlined,
    PieChartOutlined,
    FileOutlined,
    LoginOutlined,
    FormOutlined,
    FolderOpenOutlined,
    CalendarOutlined,
    FieldTimeOutlined,
    ApartmentOutlined,
    DollarOutlined
} from '@ant-design/icons';

import picture from "../MainPage/micran.svg"
import EditRegister from "../Register/EditRegister/EditRegister"


const { Header, Content, Footer, Sider } = Layout;
const { SubMenu } = Menu;


// const links = [
//     {label:'Отправка отчетов',url:}
//     {label:'Список отчетов',url:}
//     {label:,url:}
//     {label:,url:}
//     {label:,url:}
//     {label:,url:}
//     {label:,url:}
//     {label:,url:}
//     {label:,url:}
// ]

class Main extends Component{
    state = {
        collapsed: false,
        flag:true
    };
    onClickAdmin=() => {
        console.log(localStorage.getItem('menu'))
        let temp = localStorage.getItem('menu') === 'false' ? 'true' : 'false'
        localStorage.setItem('menu',temp)
    }
    onCollapse = collapsed => {
        console.log(collapsed);
        this.setState({ collapsed });
    };

    logOut = () =>{
        localStorage.setItem('token','')
        localStorage.setItem('checkReg','False')
    }

    onChangeDate = (month, dateString)=> {
        if(month !== null) {
            console.log(month, dateString)
            dateString = dateString.split('-').reverse()
            dateString[1] = parseInt(dateString[1])
            dateString = dateString.join(' ')
            localStorage.setItem('date', dateString)
            rend()
        }
    }
    onClickCalendar=(event)=>{
        console.log(event)
        // debugger;
    }
    onChangeLocation=()=>{
        let temp = document.location.pathname
        console.log(temp)
        switch (temp){
            case '/cabinet/':
                localStorage.setItem('key','0');
                break;
            case '/cabinet/salary':
                localStorage.setItem('key','1');
                break;
            case '/cabinet/salary':
                localStorage.setItem('key','2');
                break;
            case '/cabinet/list_reports':
                localStorage.setItem('key','3');
                break;
            case '/cabinet/admin/view_groups':
                localStorage.setItem('key','4');
                break;
            case '/cabinet/admin/logs':
                localStorage.setItem('key','5');
                break;
            case '/cabinet/admin/play_roll':
                localStorage.setItem('key','6');
                break;
            case '/cabinet/admin/register':
                localStorage.setItem('key','7');
                break;
            case '/cabinet/admin/employees':
                localStorage.setItem('key','8');
                break;
            case '/cabinet/admin/calendar':
                localStorage.setItem('key','9');
                break;
            case '/cabinet/admin/system_time':
                localStorage.setItem('key','10');
                break;
            case '/cabinet/admin/structure':
                localStorage.setItem('key','11');
                break;
        }
    }
    render() {

        if(!localStorage.getItem('date')){
            let date = new Date()
            localStorage.setItem('date',`${date.getMonth()>9?date.getMonth()>9+1:'0'+date.getMonth()>9} ${date.getFullYear()} `)
        }
        let a = localStorage.getItem('admin') == 'True';
        if (!localStorage.getItem('menu')){
            localStorage.setItem('menu','true')
        }
        this.onChangeLocation()
        return (

            <Layout style={{ minHeight: '100vh', paddingTop:0,margin:0 }}>
                <LogOut/>

                <Layout className="site-layout">
                    <Sider collapsible collapsed={this.state.collapsed} onCollapse={this.onCollapse} style={{backgroundColor:"white"}}>
                        <div style={{backgroundColor:"white",color:"#fff",marginTop:"20px"}}>
                            <Space direction="vertical">
                                <DatePicker
                                    size="middle"
                                    defaultValue={moment(localStorage.getItem('date').split(' ').reverse().join('-'), 'YYYY-MM')} onChange={this.onChangeDate} picker="month" />
                            </Space>
                        </div>
                        {localStorage.getItem('menu') ==='true'
                            ?<Menu defaultSelectedKeys={localStorage.getItem('key')}  onClick={this.onClickCalendar} theme="light" mode="inline">

                                <Menu.Item key="0" icon={<UpSquareOutlined style={{ fontSize: '16px'}}/>}>
                                    <a  href="http://localhost:3000/cabinet/">
                                        <span data-feather="home"></span>
                                        Отправка отчетов
                                        <span className="sr-only"></span>
                                    </a>
                                </Menu.Item>
                                <Menu.Item key="1" icon={<DollarOutlined style={{ fontSize: '16px'}}/>}>
                                    <a  href="http://localhost:3000/cabinet/salary">
                                        <span data-feather="bar-chart-2"></span>
                                        Зарплата
                                    </a>
                                </Menu.Item>
                                <Menu.Item key="2" icon={<DollarOutlined style={{ fontSize: '16px'}}/>}>
                                    <a onClick={this.onClickAdmin} href="#">
                                        <span data-feather="bar-chart-2"></span>
                                        Администрирование
                                    </a>
                                </Menu.Item>
                            </Menu>
                            :<Menu defaultSelectedKeys={localStorage.getItem('key')} mode="inline">
                                <Menu.Item key="3" icon={<UpSquareOutlined style={{ fontSize: '16px'}}/>}>
                                    <a  href="http://localhost:3000/cabinet/list_reports">
                                        <span data-feather="home"></span>
                                        Список отчетов
                                        <span className="sr-only"></span>
                                    </a>
                                </Menu.Item>
                                <Menu.Item key="4" icon={<UsergroupAddOutlined style={{ fontSize: '16px'}}/>}>
                                    <a  href='http://localhost:3000/cabinet/admin/view_groups'>
                                        <span data-feather="shopping-cart"></span>
                                        Просмотр групп
                                    </a>
                                </Menu.Item>
                                <Menu.Item key="5" icon={<LoginOutlined style={{ fontSize: '16px'}}/>}>
                                    <a  href='http://localhost:3000/cabinet/admin/logs'>
                                        <span data-feather="shopping-cart"></span>
                                        Просмотр логирования
                                    </a>
                                </Menu.Item>
                                <Menu.Item key="6" icon={<FormOutlined style={{ fontSize: '16px'}}/>}>
                                    <a href="http://localhost:3000/cabinet/admin/play_roll">
                                        <span data-feather="layers"></span>
                                        Расчетный лист
                                    </a>
                                </Menu.Item>
                                <Menu.Item key="7" icon={<FolderOpenOutlined style={{ fontSize: '16px'}}/>}>
                                    <a  href="http://localhost:3000/cabinet/admin/register">
                                        <span data-feather="layers"></span>
                                        Реестр проектов
                                    </a>
                                </Menu.Item>
                                <Menu.Item key="8" icon={<TeamOutlined style={{ fontSize: '16px'}}/>}>
                                    <a  href="http://localhost:3000/cabinet/admin/employees">
                                        <span data-feather="layers"></span>
                                        Сотрудники
                                    </a>
                                </Menu.Item>
                                <Menu.Item key="9" icon={<CalendarOutlined style={{ fontSize: '16px'}}/>}>
                                    <a  href="http://localhost:3000/cabinet/admin/calendar">
                                        <span data-feather="layers"></span>
                                        Трудовой календарь
                                    </a>
                                </Menu.Item>
                                <Menu.Item key="10" icon={<FieldTimeOutlined style={{ fontSize: '16px'}}/>}>
                                    <a  href="http://localhost:3000/cabinet/admin/system_time">
                                        <span data-feather="layers"></span>
                                        Система учета времени
                                    </a>
                                </Menu.Item>
                                <Menu.Item key="11" icon={<ApartmentOutlined style={{ fontSize: '16px'}}/>}>
                                    <a  href="http://localhost:3000/cabinet/admin/structure">
                                        <span data-feather="layers"></span>
                                        Структура подразделений
                                    </a>
                                </Menu.Item>
                                <Menu.Item key="12" icon={<ApartmentOutlined style={{ fontSize: '16px'}}/>}>
                                    <a onClick={this.onClickAdmin}  href="#">
                                        <span data-feather="layers"></span>
                                        Личный кабинет
                                    </a>
                                </Menu.Item>
                            </Menu>}
                    </Sider>
                    <Content >
                        <div className="Data" style={{backgroundColor:"white",paddingTop:"20px",minHeight:"1900px"}}>
                            {/* <LogOut clickLogOut={this.logOut}/> */}
                            <Switch>
                                <Route path='/cabinet/' exact component = {SendReport}/>
                                <Route path='/cabinet/person' exact  component = {PersonData}/>
                                <Route path='/cabinet/salary' exact  component = {Salary}/>
                                <Route path='/cabinet/admin/add_groups' exact component = {AddGroups}/>
                                <Route path='/cabinet/admin/logs' exact component = {ViewLogs}/>
                                <Route path='/cabinet/admin/view_groups' exact component = {ManageGroupps}/>
                                <Route path='/cabinet/admin/play_roll' exact  component = {Payroll}/>
                                <Route path='/cabinet/admin/register' exact  component = {Register}/>
                                <Route path='/cabinet/admin/new_project' exact  component = {NewProject}/>
                                <Route path='/cabinet/admin/edit_register' exact  component = {EditRegister}/>
                                <Route path='/cabinet/admin/employees' exact  component = {Employees}/>
                                <Route path='/cabinet/admin/calendar' exact  component = {Interval}/>
                                <Route path='/cabinet/admin/system_time' exact  component = {SystemTime}/>
                                <Route path='/cabinet/admin/structure' exact  component = {Structure}/>
                                <Route path='/cabinet/list_reports' exact  component = {ListReports}/>
                                <Route path='/cabinet/admin/edit_groups' exact component = {EditGroupps}/>
                            </Switch>
                        </div>
                    </Content>
                </Layout>
            </Layout>
        )
    }
}

export default Main;