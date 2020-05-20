import React from 'react';
import {
  H3, ProgressBar, Dialog, InputGroup, Classes, Button, Colors, Intent, FormGroup,
} from '@blueprintjs/core';
import { SPACE } from '@blueprintjs/core/lib/esm/common/keys';

import Message, { TIMEOUT } from 'utils/Message';

import 'styles/QKTView.css';
import { withStyles, makeStyles, createStyles } from '@material-ui/styles';
import { Theme, WithStyles, Paper, Grid, Typography } from '@material-ui/core';

const styles = (theme: Theme) => createStyles({
  root: {
    flexGrow: 1,
  },
  paper: {
    height: 50,
    width: 50,
    justifyContent: 'center',
    display: 'flex',
    flexDirection: 'column',
  },
});

enum Stage {
  Solving,
  Finished,
}

interface Props extends WithStyles<typeof styles> { }

interface State {
  stage: Stage;
  alpha: number[] | null;
}

/**
 * There a 3 stages:
 *   1. Inform the user what they need to do.
 *   2. Retrieval and displayment of QKTs.
 *   3. Show info after done.
 */

class QKTView extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);

    this.state = {
      stage: Stage.Finished,
      alpha: null,
    };
  }

  componentDidMount = () => {

  };

  componentWillUnmount = () => {

  };

  doneSolving = () => {
    this.setState({
      stage: Stage.Finished,
    });
  };

  onNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
  };

  onSubmit = (event: any) => {
  };

  buildGrid = (grid: number[][]) => {
    const { classes } = this.props;

    return (
      <Grid container className={classes.root}>
        <Grid item xs='auto'>{grid.map((row, r) => (
          <Grid container className={classes.root} key={r} spacing={0}>{row.map((value, c) => (
            <Grid item key={`${r}.${c}`}>
              <Paper
                className={classes.paper}
                style={{ backgroundColor: 'green' }}>
                  <Typography>
                    {value}
                  </Typography>
                </Paper>
            </Grid>
          ))}</Grid>
        ))}</Grid>
      </Grid>
    );
  };

  render = () => {
    const { stage } = this.state;
    const { classes } = this.props;

    return (
      <div>
        <FormGroup
          helperText=""
          label="composition"
          labelFor="text-input"
          labelInfo="(required)"
        >
          <InputGroup id="text-input" placeholder="1, 2, 3, 4" />
          <Button icon="arrow-right" intent={Intent.PRIMARY} />
        </FormGroup>
        {this.buildGrid([[1, 1, 1], [2, 2, 2, 2]])}
        {stage === Stage.Solving &&
          <ProgressBar
            className="sb-footer"
            value={1}
            stripes
          />
        }
      </div>
    );
  };
}

export default withStyles(styles)(QKTView);