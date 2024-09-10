import React from 'react';
import {View, Text, StyleSheet, Button} from 'react-native';
import ConfettiCannon from 'react-native-confetti-cannon';

function SuccessScreen(): React.ReactElement {
  return (
    <View style={styles.successContainer}>
      <Text style={styles.successText}>成功</Text>
      <View style={styles.answerButton}>
        <Button title="查看答案" onPress={() => {}} />
      </View>
      <ConfettiCannon
        count={200}
        origin={{x: -10, y: 0}}
        explosionSpeed={300}
        fallSpeed={2000}
        colors={['#ff0000', '#00ff00', '#0000ff']}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  successContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  successText: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  answerButton: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default SuccessScreen;