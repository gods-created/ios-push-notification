import asyncio
from typing import Callable
from loguru import logger
from mac_notifications import client as notification
from functools import partial

from modules.worker import Worker

async def main(target_price: str) -> Callable[..., None]:
    async with Worker() as worker:
        response = await worker._executing()
        
    if response.get('status', 'error') == 'error':
        logger.debug(response)
        return None
        
    price = response.get('price', 0.00)
    try:
        if price > float(target_price):
            notification.create_notification(
                title='WARNING!!!',
                subtitle='The current price is more than target!',
                sound='Frog',
                action_button_str='Open website',
                action_callback=partial(Worker.open_browser)
            )
        
    except ValueError as e:
        logger.error('Target price is invalid!')
    
    finally:
        return None
        
def job() -> Callable[..., None]:
    target_price = input('')
        
    try:
        asyncio.run(main(target_price))
        
    except KeyboardInterrupt:
        logger.info('\Exit')
        
    except Exception as e:
        logger.error(str(e))
        
    finally:
        return job()
    
if __name__ == '__main__':
    job()

