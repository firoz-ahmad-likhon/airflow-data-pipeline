from typing import cast
import pytest
import great_expectations as gx
from great_expectations.data_context import AbstractDataContext
from quality.gx_init import GXInitiator


@pytest.fixture(scope="session")
def gxi() -> type[GXInitiator]:
    """Fixture to initialize a GX context for integration tests.

    This fixture sets up the necessary directories and initializes
    the Great Expectations context using `GXInitiator`.

    Returns:
        The `GXInitiator` class.

    """
    # Initialize Great Expectations
    GXInitiator.initialize("init")

    return cast(type[GXInitiator], GXInitiator)


@pytest.fixture(scope="session")
def context(gxi: GXInitiator) -> AbstractDataContext:
    """Fixture to provide an AbstractDataContext for integration tests.

    This fixture uses the directory set up by the `gxi` fixture.

    Args:
        gxi: The GXInitiator fixture providing the project directory.

    Returns:
        A Great Expectations AbstractDataContext initialized with the project directory.

    """
    return gx.get_context(
        mode="file",
        project_root_dir=str(gxi.PROJECT_DIR),
    )  # Use the directory set by `gxi`


@pytest.fixture(scope="session")
def dimensions() -> list[str]:
    """List of dimensions for suites, validation definitions.

    returns: A list of Great Expectations suites.
    """
    return ["distribution", "missingness", "schema", "volume"]


@pytest.fixture(scope="session")
def checkpoints() -> list[str]:
    """List of available checkpoints.

    returns: A list of Great Expectations checkpoints.
    """
    return ["statistical_checkpoint", "completeness_checkpoint"]
