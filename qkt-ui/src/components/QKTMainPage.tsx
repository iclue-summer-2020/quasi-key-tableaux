import React from 'react';
import dotenv from 'dotenv';

import QKTView from 'components/QKTView';


dotenv.config();

const { REACT_APP_QKT_HOST = 'localhost', REACT_APP_QKT_PORT = 9000 } = process.env;


const QKTMainPage = () => (
  <QKTView />
);

export default QKTMainPage;