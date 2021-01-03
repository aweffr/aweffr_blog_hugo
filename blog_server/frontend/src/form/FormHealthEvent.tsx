import React, {useState} from 'react';
import {Form, FormGroup, Input, Label} from "reactstrap";
import './FormHealthEvent.scss';

const FormHealthEvent: React.FC = (props) => {

  const [heartRate, setHeartRate] = useState('');
  const [calories, setCalories] = useState('');

  return (
    <div>
      <FormGroup className='test'>
        <Label for='heartRate'>心率</Label>
        <Input id='heartRate' value={heartRate} onChange={evt => setHeartRate(evt.target.value)}/>
      </FormGroup>
      <FormGroup className='test'>
        <Label for='calories'>卡路里</Label>
        <Input id='calories' value={calories} onChange={evt => setCalories(evt.target.value)}/>
      </FormGroup>
    </div>
  );
};


export default FormHealthEvent;
