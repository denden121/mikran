import React from "react"
import {Card,Col,Row,Button,Select,Input} from "antd"

const gridStyle = {
    width: '100%',
    textAlign: 'left',
  };
const { TextArea } = Input;

const ReportModal =(props)=>{
    return(
        <div className="container-fluid">
            <div className="row">
                <div className="col-lg-12">
                    <div className="list-group-item list-group-item-action list-group-item-danger">Отчет заблокирован руководителем</div>
                    <br/>
                    <div className="site-card-wrapper">
                        <Row gutter={16}>
                            <Col span={10}>
                                <Card title="Список проектов" bordered={true}>
                                    <Card.Grid style={gridStyle}>
                                        <div className="row">
                                            <div className="col-lg-6">
                                                <div style={{padding:"15px"}} className="text-left"><strong>№1</strong></div>
                                            </div>
                                            <div className="col-lg-6">
                                                <div style={{padding:"15px",color:"red"}} className="text-right">12ч</div>
                                            </div>
                                        </div>
                                                                          
                                    <div className="text-right" style={{paddingRight:"5px",paddingBottom:"10px"}}>
                                        <Button  type="primary" danger size="small">
                                            Удалить
                                        </Button>
                                    </div>
                                    </Card.Grid>
                                    <Card.Grid style={gridStyle}></Card.Grid>
                                    <Card.Grid style={gridStyle}></Card.Grid>
                                </Card>
                                <br/>
                                    <div className="row">
                                        <div className="col-lg-12 text-right">
                                            <button className="btn btn-success btn-sm">Добавить проект</button>
                                        </div>
                                    </div>
                                <br/>
                                <div className="row">
                                    <div className="col-lg-12 text-right" style={{color:"#40D0E3",fontSize:"20px"}}>
                                        13.80 ч.
                                    </div>
                                </div>
                                <div className="row">
                                    <div className="col-lg-12 text-right" style={{color:"grey"}}>
                                        Итого
                                    </div>
                                </div>
                                <br/>
                                <div className="row">
                                    <div className="col-lg-12 text-right" style={{color:"#40D0E3",fontSize:"20px"}}>
                                        48.52 ч.
                                    </div>
                                </div>
                                <div className="row">
                                    <div className="col-lg-12 text-right" style={{color:"grey"}}>
                                        Время по карточке
                                    </div>
                                </div>
                            </Col>
                            <Col span={14}>
                                <Card  bordered={true}>
                                    <div className="row">
                                        <div className="col-lg-12 text-left">
                                            <strong>Проект:</strong>
                                        </div>
                                        <br/>
                                        <div className="col-lg-12">
                                            <Select
                                            style={{width:"100%"}}/>
                                        </div>
                                    </div>
                                    <br/>
                                    <div className="row">
                                        <div className="col-lg-12 text-left">
                                            <strong>Часы:</strong>
                                        </div>
                                        <br/>
                                        <div className="col-lg-12">
                                            <Input
                                            style={{width:"100%"}}/>
                                        </div>
                                    </div>
                                    <br/>
                                    <div className="row">
                                        <div className="col-lg-12 text-left">
                                            <strong>Комментарии:</strong>
                                        </div>
                                        <br/>
                                        <div className="col-lg-12">
                                        <TextArea
                                        // value={value}
                                        autoSize={{ minRows: 10, maxRows: 20 }}
                                        style={{width:"100%"}}
                                    />
                                        </div>
                                    </div>
                                    <br/>
                                    <div className="row">
                                        <div className="col-lg-12 text-right">
                                            <button className="btn btn-success btn-sm">Сохранить</button>
                                        </div>
                                    </div>
                                </Card>
                            </Col>                        
                        </Row>
                     </div>
                </div>
            </div>
        </div>
    )
}

export default ReportModal